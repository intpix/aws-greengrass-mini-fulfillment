#!/usr/bin/env bash

python servode.py write_register torque_enable 1 --sid 20
python servode.py write_register torque_enable 1 --sid 21
python servode.py write_register torque_enable 1 --sid 22
python servode.py write_register torque_enable 1 --sid 23
python servode.py write_register torque_enable 1 --sid 24
python servode.py write_register torque_limit 1023 --sid 20
python servode.py write_register torque_limit 1023 --sid 21
python servode.py write_register torque_limit 1023 --sid 22
python servode.py write_register torque_limit 1023 --sid 23
python servode.py write_register torque_limit 1023 --sid 24
python servode.py write_register cw_compliance_slope 400 --sid 20
python servode.py write_register cw_compliance_slope 400 --sid 21
python servode.py write_register cw_compliance_slope 400 --sid 22
python servode.py write_register cw_compliance_slope 400 --sid 23
python servode.py write_register cw_compliance_slope 400 --sid 24
python servode.py write_register ccw_compliance_slope 400 --sid 20
python servode.py write_register ccw_compliance_slope 400 --sid 21
python servode.py write_register ccw_compliance_slope 400 --sid 22
python servode.py write_register ccw_compliance_slope 400 --sid 23
python servode.py write_register ccw_compliance_slope 400 --sid 24
python servode.py write_register moving_speed 200 --sid 20
python servode.py write_register moving_speed 200 --sid 21
python servode.py write_register moving_speed 200 --sid 22
python servode.py write_register moving_speed 200 --sid 23
python servode.py write_register moving_speed 200 --sid 24
python servode.py write_register cw_compliance_margin 1 --sid 20
python servode.py write_register cw_compliance_margin 1 --sid 21
python servode.py write_register cw_compliance_margin 1 --sid 22
python servode.py write_register cw_compliance_margin 1 --sid 23
python servode.py write_register cw_compliance_margin 1 --sid 24
python servode.py write_register ccw_compliance_margin 1 --sid 20
python servode.py write_register ccw_compliance_margin 1 --sid 21
python servode.py write_register ccw_compliance_margin 1 --sid 22
python servode.py write_register ccw_compliance_margin 1 --sid 23
python servode.py write_register ccw_compliance_margin 1 --sid 24
