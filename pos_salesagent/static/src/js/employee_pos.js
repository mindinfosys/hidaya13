odoo.define('agent_performance_analysis.employee_pos', function (require) {
    "use strict";
    var screens = require('point_of_sale.screens');
    var gui = require('point_of_sale.gui');
    var core = require('web.core');
    var rpc = require('web.rpc');
    var PopupWidget = require('point_of_sale.popups');
    var _t = core._t;
    var models = require('point_of_sale.models');

    models.load_models({
        model: 'hr.employee',
        fields: ['id', 'name'],
        domain: function(){ return [['is_a_agent','=',true]]; },
        loaded: function (self, employee) {
            self.employee_name_by_id = {};
            for (var i = 0; i < employee.length; i++) {
                self.employee_name_by_id[employee[i].id] = employee[i];
            }
        }
    });

    var _super_order = models.Order.prototype;
    models.Order = models.Order.extend({
        export_as_JSON: function () {
            var json = _super_order.export_as_JSON.apply(this, arguments);
            json.order_agent = this.order_agent;
            json.agent_id = this.agent_id;
            return json;
        },
        init_from_JSON: function (json) {
            _super_order.init_from_JSON.apply(this, arguments);
            this.order_agent = json.order_agent;
            this.agent_id = json.agent_id;
            _super_order.init_from_JSON.call(this, json);
        }
    });

    var AgentPopupWidget = PopupWidget.extend({
        template: 'AgentPopupWidget',
        init: function (parent, options) {
            this.options = options || {};
            this._super(parent, _.extend({}, {
                size: "medium"
            }, this.options));
        },
        renderElement: function () {
            this._super();
            for (var employee in this.pos.employee_name_by_id) {
                $('#employee_select').append($("<option>" + this.pos.employee_name_by_id[employee].name + "</option>").attr("value", this.pos.employee_name_by_id[employee].name).attr("id", this.pos.employee_name_by_id[employee].id))
            }
        },
        click_confirm: function () {
            var employee_id = $("#employee_select :selected").attr('id');
            var employee_name = $("#employee_select :selected").text();
            var order = this.pos.get_order();
            order.order_agent = employee_name;
            order.agent_id = employee_id;
            this.gui.close_popup();
        },

    });
    gui.define_popup({name: 'pos_no', widget: AgentPopupWidget});

    var AgentSelectionButton = screens.ActionButtonWidget.extend({
        template: 'AgentSelectionButton',
        button_click: function () {
            var note = this.pos.get_order().order_agent;
            this.gui.show_popup('pos_no', {'value': this.pos.get_order().order_agent});
        }
    });

    screens.define_action_button({
        'name': 'pos_agent_selection',
        'widget': AgentSelectionButton,
        'condition': function(){
        return this.pos.config.agent_configuration;
    }
    });
});

