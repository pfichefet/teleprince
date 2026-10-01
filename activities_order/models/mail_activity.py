from odoo import api, models


class MailActivity(models.Model):
    _inherit = "mail.activity"

    @api.readonly
    @api.model
    def get_activity_data(self, res_model, domain, limit=None, offset=0, fetch_done=False):
        res = super().get_activity_data(res_model, domain, limit=limit, offset=offset, fetch_done=fetch_done)
        grouped_activities = res["grouped_activities"]

        # Closest deadline of the ongoing activities of each record
        res_id_to_deadline = {}
        for res_id, by_type in grouped_activities.items():
            deadlines = [
                data["reporting_date"]
                for data in by_type.values()
                if data["state"] != "done" and data["reporting_date"]
            ]
            if deadlines:
                res_id_to_deadline[res_id] = min(deadlines)

        # Records with ongoing activities ordered by deadline DESC (instead of ASC),
        # records with only completed activities are kept at the end in the original order
        ongoing_res_ids = sorted(res_id_to_deadline, key=lambda r: res_id_to_deadline[r], reverse=True)
        completed_res_ids = [r for r in res["activity_res_ids"] if r not in res_id_to_deadline]
        res["activity_res_ids"] = ongoing_res_ids + completed_res_ids
        return res
