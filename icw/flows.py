from viewflow import flow
from viewflow.activation import Activation
from viewflow.base import Flow, this
import viewflow.frontend
from viewflow.flow.views import UpdateProcessView

from . import models, views


@viewflow.frontend.register
class ModerateAccidentFlow(Flow):
    process_class = models.AccidentPendingModeration

    start = flow.StartFunction(this.start_flow).Next(this.approve)

    approve = flow.View(UpdateProcessView, fields=['approved']).Permission('icw.moderate_accident').Next(this.check_approve)

    check_approve = flow.If(lambda activation: activation.process.approved).Then(this.approved).Else(this.end)

    end = flow.End()

    def start_flow(self, activation: Activation):
        activation.prepare()
        activation.done()
        return activation

    @flow.Handler
    def approved(self, activation):
        pass

    class Meta:
        view_permission_name = 'icw.moderate_accident'
