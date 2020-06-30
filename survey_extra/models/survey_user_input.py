# -*- coding: utf-8 -*-
from odoo import api, exceptions, fields, models

import logging
_logger = logging.getLogger(__name__)

class SurveyUserinput(models.Model):
    _inherit = 'survey.user_input'

    date_done = fields.Datetime(
        string="Fecha fin"
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Comercial'
    )
    user_id_done = fields.Many2one(
        comodel_name='res.users',
        string='Comercial hecho'
    )
    survey_id_survey_type = fields.Char(
        compute='_survey_id_survey_type',
        string="Tipo de encuesta",
        readonly=True
    )
    survey_url = fields.Char(
        compute='_survey_url',
        string="Url",
        readonly=True
    )
    partner_id_phone = fields.Char(
        compute='_partner_id_phone',
        string="Telefono",
        readonly=True
    )
    partner_id_mobile = fields.Char(
        compute='_partner_id_mobile',
        string="Movil",
        readonly=True
    )

    @api.depends('survey_id')
    def _survey_id_survey_type(self):
        for item in self:
            item.survey_id_survey_type = item.survey_id.survey_type

    @api.depends('survey_id')
    def _survey_url(self):
        web_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for item in self:
            item.survey_url = str(web_base_url) + '/survey/fill/' + str(item.survey_id.id) + '/' + str(item.token)

    @api.depends('partner_id')
    def _partner_id_phone(self):
        for item in self:
            item.partner_id_phone = item.partner_id.phone

    @api.depends('partner_id')
    def _partner_id_mobile(self):
        for item in self:
            item.partner_id_mobile = item.partner_id.mobile

    @api.model
    def action_boton_pedir_llamada(self):
        response = {
            'errors': True,
            'error': "No tienes respuesta de llamada para poder asignarte"
        }
        # survey_user_input_ids
        survey_user_input_ids = self.env['survey.user_input'].search(
            [
                ('type', '=', 'manually'),
                ('survey_id.survey_type', '=', 'phone'),
                ('state', 'not in', ('done', 'expired')),
                ('user_id', '=', False),
                ('test_entry', '=', False)
            ],
            order='date_create asc'
        )
        if len(survey_user_input_ids) > 0:
            survey_user_input_id = survey_user_input_ids[0]
            survey_user_input_id.user_id = self._uid

            response['errors'] = False
            # return
        return response

    @api.multi
    def write(self, vals):
        # stage date_done
        if vals.get('state') == 'done' and self.date_done == False:
            vals['date_done'] = fields.datetime.now()
            # user_id_done
            context = self._context
            if 'uid' in context:
                vals['user_id_done'] = context.get('uid')
        # write
        return super(SurveyUserinput, self).write(vals)