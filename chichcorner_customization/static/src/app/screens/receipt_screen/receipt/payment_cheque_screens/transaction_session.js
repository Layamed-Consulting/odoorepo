/** @odoo-module **/

import { ClosePosPopup } from "@point_of_sale/app/navbar/closing_popup/closing_popup";
import { patch } from "@web/core/utils/patch";

//const OriginalCloseSession = ClosePosPopup.prototype.closeSession;

patch(ClosePosPopup.prototype, {
    async closeSession() {
        const sessionId = this.pos.pos_session.id;
        const notes = this.state.notes || "";
        const cashierName = this.pos.cashier.name;
        const storeName = this.pos.config.name;
        const cashDetails = this.props.default_cash_details;
        const cashExpected = parseFloat(cashDetails.amount || 0);
        const cashCounted = parseFloat(this.state.payments[cashDetails.id]?.counted || 0);
        //const cashDifference = this.getDifference(); // Use getMaxDifference for cash
        const cashDifference = cashCounted - cashExpected;

        const paymentMethodsData = [
            {
                session_id: sessionId,
                payment_method_id: cashDetails.id,
                cashier_name: cashierName, // Add cashier's name
                store_name: storeName,
                payment_method_name: cashDetails.name,
                expected: cashExpected,
                counted_cash: cashCounted,
                payment_differences: cashDifference,
                notes: notes,
            },
            ...this.props.other_payment_methods.map(paymentMethod => {
                const expected = parseFloat(paymentMethod.amount || 0);
                const counted = parseFloat(this.state.payments[paymentMethod.id]?.counted || 0);
                const difference =  counted - expected;

                return {
                    session_id: sessionId,
                    payment_method_id: paymentMethod.id,
                    cashier_name: cashierName, // Add cashier's name
                    store_name: storeName,
                    payment_method_name: paymentMethod.name,
                    expected: expected,
                    counted_cash: counted,
                    payment_differences: difference,
                    notes: notes,
                };
            }),
        ];
        for (const paymentMethodData of paymentMethodsData) {
            try {
                await this.orm.call("transaction.session", "create", [paymentMethodData]);
                console.log("Transaction session data saved successfully:", paymentMethodData);
            } catch (error) {
                console.error("Failed to save transaction session data:", error);
            }
        }

        window.location = "/web#action=point_of_sale.action_client_pos_menu";
    },
});
