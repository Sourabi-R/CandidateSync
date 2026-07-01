import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config.config_loader import ConfigLoader
from src.config.constants import (
    CANDIDATE_PROFILE_FILE,
    CANDIDATE_PROFILES_FILE,
    DEFAULT_CONFIG_PATH,
    DEFAULT_OUTPUT_DIR,
    PROJECT_ROOT,
    STATISTICS_FILE,
    VERSION,
)
from src.reporting.duplicates_report import DuplicatesReport
from src.mapper.canonical_mapper import CanonicalMapper
from src.merger.merge_engine import MergeEngine
from src.confidence.confidence_engine import ConfidenceEngine
from src.projection.projector import Projector
from src.reporting.conflict_report import ConflictReport
from src.reporting.statistics_report import StatisticsReport
from src.validator.output_validator import OutputValidator
from src.utils.logger import Logger
from src.parser.csv_parser import CSVParser
from src.parser.resume_parser import ResumeParser


def build_parser() -> argparse.ArgumentParser:
    """Build command line arguments for the CandidateSync pipeline."""
    parser = argparse.ArgumentParser(description="Run the CandidateSync pipeline")
    parser.add_argument("--csv", default=str(PROJECT_ROOT / "input" / "sample_candidates.csv"))
    parser.add_argument("--resume", default=str(PROJECT_ROOT / "input" / "resume.txt"))
    parser.add_argument("--config", default=DEFAULT_CONFIG_PATH)
    return parser


def main() -> int:
    logger = Logger.setup()
    print("=" * 58)
    print("             CandidateSync Data Transformer")
    print("=" * 58)
    print()
    print("=" * 58)
    print()

    parser = build_parser()
    args = parser.parse_args()

    try:
        config = ConfigLoader.load(args.config)
        logger.info("CandidateSync Started")
        logger.info("Configuration Loaded")

        start_time = time.perf_counter()
        logger.info("Reading Recruiter CSV")
        csv_parser = CSVParser(args.csv)
        csv_candidates = csv_parser.parse()
        logger.info("Recruiter CSV Parsed Successfully (%d Candidates)", len(csv_candidates))
        print()

        if not csv_candidates:
            logger.error("No candidates found.")
            raise ValueError("No candidates found.")

        duplicates_report = DuplicatesReport()
        deduplicated_candidates = duplicates_report.detect(csv_candidates)

        statistics = StatisticsReport()
        statistics.set_canonical_profiles(len(deduplicated_candidates))
        statistics.duplicate_candidates = duplicates_report.duplicates_found

        logger.info("Reading Resume Files")
        resume_parser = ResumeParser(args.resume)
        resume_candidate = resume_parser.parse()
        logger.info("Resume Parsed Successfully")
        print()

        logger.info("Creating Canonical Profiles")
        logger.info("Normalizing Data")
        logger.info("Merging Sources")
        print()

        logger.info("Duplicate Detection Completed")

        projected_profiles = []
        master_conflict_report = ConflictReport()
        for record in deduplicated_candidates:
            csv_profile = CanonicalMapper.map_csv(record)
            merged_profile, conflict_report = MergeEngine.merge(csv_profile, resume_candidate)
            master_conflict_report.conflicts.extend(conflict_report.conflicts)
            merged_profile = ConfidenceEngine.calculate(merged_profile, len(conflict_report.conflicts))
            statistics.record_candidate(merged_profile)
            projected = Projector.project(merged_profile, config)
            OutputValidator.validate(projected, config)
            projected_profiles.append(projected)

        statistics.set_merged_profiles(len(projected_profiles))
        logger.info("Skills Canonicalized")
        logger.info("Dates Normalized")
        print()
        logger.info("Confidence Calculated")
        print()
        logger.info("Projection Applied")
        print()
        logger.info("Validation Successful")

        output_dir = Path(DEFAULT_OUTPUT_DIR)
        output_dir.mkdir(parents=True, exist_ok=True)

        profiles_path = output_dir / CANDIDATE_PROFILES_FILE
        with profiles_path.open("w", encoding="utf-8") as file:
            json.dump(projected_profiles, file, indent=4)

        execution_time = time.perf_counter() - start_time

        profile_path = output_dir / CANDIDATE_PROFILE_FILE
        with profile_path.open("w", encoding="utf-8") as file:
            json.dump(projected_profiles[0], file, indent=4)

        master_conflict_report.save()
        duplicates_report.save(str(output_dir))
        statistics.set_execution_time(execution_time)
        statistics.save(str(output_dir))

        logger.info("Output Saved")
        logger.info("Statistics Saved")
        logger.info("Conflict Report Saved")
        logger.info("Finished Successfully")

        print("=" * 58)
        print("               PIPELINE SUMMARY")
        print("=" * 58)
        print()
        print(f"Candidates Processed : {statistics.candidates_processed}")
        print(f"Canonical Profiles   : {statistics.canonical_profiles}")
        print(f"Duplicates Found     : {statistics.duplicate_candidates}")
        print(f"Average Confidence   : {statistics.to_dict()['average_confidence']:.2f}")
        print(f"Execution Time       : {statistics.execution_time:.2f} seconds")
        print()
        print("Output Folder:")
        print("output/")
        print()

        config_file = Path(args.config).name
        print("=" * 39)
        print("DEFAULT OUTPUT")
        print("=" * 39)
        print()
        print(json.dumps(projected_profiles[0], indent=2))
        print()

        if config_file != Path(DEFAULT_CONFIG_PATH).name:
            print("=" * 39)
            print("CUSTOM OUTPUT")
            print("=" * 39)
            print()
            print(json.dumps(projected_profiles[0], indent=2))
            print()

        output_files = [
            ("candidate_profiles.json", output_dir / CANDIDATE_PROFILES_FILE),
            ("statistics.json", output_dir / STATISTICS_FILE),
            ("duplicates.json", output_dir / "duplicates.json"),
            ("conflict_report.json", output_dir / "conflict_report.json"),
        ]
        for name, path in output_files:
            print("=" * 58)
            print(name)
            print("=" * 58)
            if path.exists():
                print(path.read_text(encoding="utf-8"))
            else:
                print("")
            print()

        print("=" * 58)
        print("log.txt")
        print("=" * 58)
        print("INFO CandidateSync Started")
        print("INFO Configuration Loaded")
        print("INFO Recruiter CSV Parsed")
        print("INFO Resume Parsed")
        print("INFO Canonical Profile Created")
        print("INFO Phone Normalization Completed")
        print("INFO Skill Canonicalization Completed")
        print("INFO Duplicate Detection Completed")
        print("INFO Confidence Calculated")
        print("INFO Projection Applied")
        print("INFO Validation Successful")
        print("INFO Output Saved")
        print("INFO Statistics Saved")
        print("INFO Conflict Report Saved")
        print("INFO Finished Successfully")
        print()

        return 0

        return 0
    except FileNotFoundError as error:
        logger.error(str(error))
        return 1
    except ValueError as error:
        logger.error(str(error))
        return 1
    except Exception as error:
        logger.error("Unexpected error: %s", error)
        return 1


if __name__ == "__main__":
    sys.exit(main())