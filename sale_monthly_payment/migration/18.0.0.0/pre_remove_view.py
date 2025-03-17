import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    cr.execute("DELETE FROM ir_ui_view WHERE arch_prev LIKE 'line_taxed_total'")
    _logger.info("Remove %s views with line_taxed_total", cr.rowcount)
