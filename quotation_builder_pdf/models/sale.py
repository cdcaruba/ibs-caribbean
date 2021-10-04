# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from bs4 import BeautifulSoup

TEXT_ATTRIBUTES = ['Title', 'Text block', 'Separator', 'Image - Text', 'Text - Image', 'Picture']


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    x_txt_website_description = fields.Html('Text Website Description', compute='_sanitize_html',
                                            sanitize_attributes=False)


    @api.depends('website_description')
    def _sanitize_html(self):
        for record in self:
            text = record.website_description
            if text:
                soup = BeautifulSoup(text, 'lxml')
                for widget in soup.find_all('section'):
                    if widget.get('data-name') and widget['data-name'] not in TEXT_ATTRIBUTES:
                        widget.decompose()
                for div in soup.find_all('div', title="Pagebreak"):
                    div.decompose()
                for div in soup.find_all('div'):
                    if div.get('data-name') and div['data-name'] == 'Separator':
                        div.clear()
                        div['style'] = "page-break-after: always;"
                    # We convert all bootstrap grid classes to general sizes so that they apply to the PDF (i.e. col-lg-6 -> col-6)
                    classes = []
                    for c in div.get('class'):
                        if c.startswith('col-'):
                            classes.append('col-' + ''.join([digit for digit in c if digit.isdigit()]))
                        else:
                            classes.append(c)
                    div['class'] = classes

                record['x_txt_website_description'] = soup.prettify()
            else:
                record['x_txt_website_description'] = ''


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    x_txt_website_description = fields.Html('Text Website Description', compute='_sanitize_html',
                                            sanitize_attributes=False)


    @api.depends('website_description')
    def _sanitize_html(self):
        for record in self:
            text = record.website_description
            if text:
                soup = BeautifulSoup(text, 'lxml')
                for widget in soup.find_all('section'):
                    if widget.get('data-name') and widget['data-name'] not in TEXT_ATTRIBUTES:
                        widget.decompose()
                for div in soup.find_all('div', title="Pagebreak"):
                    div.decompose()
                for div in soup.find_all('div'):
                    if div.get('data-name') and div['data-name'] == 'Separator':
                        div.clear()
                        div['style'] = "page-break-after: always;"
                    # We convert all bootstrap grid classes to general sizes so that they apply to the PDF (i.e. col-lg-6 -> col-6)
                    classes = []
                    for c in div.get('class'):
                        if c.startswith('col-'):
                            classes.append('col-' + ''.join([digit for digit in c if digit.isdigit()]))
                        else:
                            classes.append(c)
                    div['class'] = classes


                record['x_txt_website_description'] = soup.prettify()
            else:
                record['x_txt_website_description'] = ''
