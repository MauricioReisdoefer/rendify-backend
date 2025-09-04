from flask import Blueprint
from Controllers.simulator_controller import (
    add_or_update_simulator,
    get_simulator,
    get_all_simulators,
    delete_simulator,
    restart
)

simulator_bp = Blueprint("simulator_bp", __name__, url_prefix="/simulator")

simulator_bp.route("/add", methods=["POST"])(add_or_update_simulator)
simulator_bp.route("/get/<string:symbol>", methods=["GET"])(get_simulator)
simulator_bp.route("/", methods=["GET"])(get_all_simulators)
simulator_bp.route("/delete/<string:symbol>", methods=["DELETE"])(delete_simulator)
simulator_bp.route("/restart", methods=["DELETE"])(restart)