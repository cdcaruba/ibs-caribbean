# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from lxml import html

TEXT_ATTRIBUTES = ['Title', 'Text block', 'Separator', 'Image - Text', 'Text - Image', 'Picture', 'Columns']


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    x_txt_website_description = fields.Html('Text Website Description', compute='_sanitize_html',
                                            sanitize_attributes=False)

    @api.depends('website_description')
    def _sanitize_html(self):
        for record in self:
            text = record.website_description
            if not text:
                record.x_txt_website_description = ''
            else:
                tree = html.fromstring(text)

                # Widgets in the web editor are the <section> nodes with data-name attribute
                # We need to find and remove the ones that are not in the allowed list
                for widget in tree.xpath('//section[@data-name]'):
                    if widget.get('data-name') not in TEXT_ATTRIBUTES:
                        widget.getparent().remove(widget)

                for div in tree.xpath('//div'):
                    if div.get('title') and div.get('title') == 'Pagebreak':
                        div.getparent().remove(div)
                        continue

                    # Use Separator widget to simulate a page break
                    # so that the user can manually add them when designing the template
                    if div.get('data-name') and div.get('data-name') == 'Separator':
                        div.clear()
                        div.set('style', 'page-break-after: always;')

                    # We convert all bootstrap grid classes to general sizes so that they apply to the PDF (i.e. col-lg-6 -> col-6)
                    classes = []
                    for c in div.classes:
                        if c.startswith('col-'):
                            classes.append('col-' + ''.join([digit for digit in c if digit.isdigit()]))
                        else:
                            classes.append(c)
                    if classes:
                        div.set('class', ' '.join(classes))

                record.x_txt_website_description = html.tostring(tree, pretty_print=True)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    x_txt_website_description = fields.Html('Text Website Description', compute='_sanitize_html',
                                            sanitize_attributes=False)

    @api.depends('website_description')
    def _sanitize_html(self):
        for record in self:
            text = record.website_description
            if not text:
                record.x_txt_website_description = ''
            else:
                tree = html.fromstring(text)

                # Widgets in the web editor are the <section> nodes with data-name attribute
                # We need to find and remove the ones that are not in the allowed list
                for widget in tree.xpath('//section[@data-name]'):
                    if widget.get('data-name') not in TEXT_ATTRIBUTES:
                        widget.getparent().remove(widget)

                for div in tree.xpath('//div'):
                    if div.get('title') and div.get('title') == 'Pagebreak':
                        div.getparent().remove(div)
                        continue

                    # Use Separator widget to simulate a page break
                    # so that the user can manually add them when designing the template
                    if div.get('data-name') and div.get('data-name') == 'Separator':
                        div.clear()
                        div.set('style', 'page-break-after: always;')

                    # We convert all bootstrap grid classes to general sizes so that they apply to the PDF (i.e. col-lg-6 -> col-6)
                    classes = []
                    for c in div.classes:
                        if c.startswith('col-'):
                            classes.append('col-' + ''.join([digit for digit in c if digit.isdigit()]))
                        else:
                            classes.append(c)
                    if classes:
                        div.set('class', ' '.join(classes))

                record.x_txt_website_description = html.tostring(tree, pretty_print=True)