from dataclasses import dataclass, field
from typing import List

import click

from src.hardshell.common.common import log_status


@dataclass
class Report:
    checks_failed: int = 0
    checks_passed: int = 0
    checks_skipped: int = 0
    entries: List[int] = field(default_factory=list)
    title: str = "hardshell report"

    def add_entry(self, result):
        self.entries.append(result)

    def generate_summary(self):
        checks_failed = 0
        checks_passed = 0
        checks_skipped = 0
        summary = f"{self.title}\n" + "=" * len(self.title) + "\n"
        for entry in self.entries:
            if entry.get("result") == "pass":
                checks_passed += 1
            elif entry.get("result") == "skip":
                checks_skipped += 1
            elif entry.get("result") == "fail":
                checks_failed += 1

            summary += (
                f"check name: {str(entry.get('name'))}"
                + "\t"
                + f"check id: {str(entry.get('id'))}"
                + "\t"
                + f"check type: {str(entry.get('type'))}"
                + "\t"
                + f"check subtype: {str(entry.get('subtype'))}"
                + "\t"
                + f"check result: {str(entry.get('result'))}"
                + "\n"
            )

        summary += f"\nchecks passed: {checks_passed}\nchecks failed: {checks_failed}\nchecks skipped: {checks_skipped}\n"

        return summary

    def get_entries(self):
        return self.entries

    def get_check_results_total(self):
        return self.checks_passed, self.checks_failed, self.checks_skipped

    def get_check_results_total_formatted(self):
        for result in self.entries:
            if result.get("result") == "pass":
                self.checks_passed += 1
            elif result.get("result") == "skip":
                self.checks_skipped += 1
            elif result.get("result") == "fail":
                self.checks_failed += 1

        click.echo(click.style("#" * 90 + "\n", fg="blue"))
        click.echo(
            click.style(
                f"checks passed: {str(self.checks_passed)}, checks failed: {str(self.checks_failed)}, checks skipped: {str(self.checks_skipped)}",
                fg="green",
            )
        )

    def export_to_txt(self, file_path):
        with open(file_path, "w") as file:
            file.write(self.generate_summary())

    def export_to_html(self, file_path):
        html_content = f"<html><head><title>{self.title}</title></head><body>"
        html_content += f"<h1>{self.title}</h1><ul>"
        for entry in self.entries:
            html_content += f"<li>{entry}</li>"
        html_content += "</ul></body></html>"
        with open(file_path, "w") as file:
            file.write(html_content)
