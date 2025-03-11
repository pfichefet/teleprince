# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models


class TaskCustomReportNoTS(models.AbstractModel):
    _name = "report.task_report_no_timesheet.worksheet_custom_no_ts"
    _description = "Worksheet Custom Report Without Timesheet"

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env["project.task"].browse(docids).sudo()
        data = {
            "doc_ids": docids,
            "doc_model": "project.task",
            "docs": docs,
        }
        worksheet_map = {}
        for task in data.get("docs"):
            if task.worksheet_template_id:
                x_model = task.worksheet_template_id.model_id.model
                worksheet = self.env[x_model].search(
                    [("x_project_task_id", "=", task.id)],
                    limit=1,
                    order="create_date DESC",
                )  # take the last one
                worksheet_map[task.id] = worksheet

        data.update({"worksheet_map": worksheet_map})
        return data
