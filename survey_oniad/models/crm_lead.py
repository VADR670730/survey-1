# -*- coding: utf-8 -*-
from openerp import _, api, exceptions, fields, models
from openerp.exceptions import Warning

import logging
_logger = logging.getLogger(__name__)

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    @api.model
    def get_survey_id(self):
        survey_id = 0
        if self.lead_oniad_type!=False:            
            survey_survey_ids = self.env['survey.survey'].search(
                [
                    ('survey_lead_oniad_type', '=', self.lead_oniad_type),
                    ('survey_type', '=', 'popup'),
                    ('survey_subtype', '=', 'why_not'),
                    ('active', '=', True)
                ]
            )
            if len(survey_survey_ids)>0:
                survey_survey_id = survey_survey_ids[0]
                survey_id = survey_survey_id.id            
                    
        return survey_id