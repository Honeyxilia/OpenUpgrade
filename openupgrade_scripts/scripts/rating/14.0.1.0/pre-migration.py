# Copyright 2021 Tecnativa - Pedro M. Baeza
# Copyright 2021 ForgeFlow S.L.  <https://www.forgeflow.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


def update_rating_value(env):
    # range changed from 0-10 to 0-5
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE rating_rating
        SET rating = round(rating / 2.0)
        WHERE rating IS NOT NULL
        AND res_model != 'project.task'
        """,
    )


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_xmlids(
        env.cr, [("rating.action_view_rating", "rating.rating_rating_view")]
    )
    _logger.info(
        "[Commown OpenUpgrade fork - rating pre-migration]"
        " Score halving disabled for project.task ratings"
    )
    update_rating_value(env)
