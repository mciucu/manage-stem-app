import {UI, CodeEditor} from "UI";

import {Ajax} from "base/Ajax";
import {ensure} from "base/Require";
import {getCookie} from "base/Utils";
import {PageTitleManager} from "base/PageTitleManager";
import {WebsocketSubscriber} from "websocket/WebsocketSubscriber";

import {GlobalState} from "state/State";

PageTitleManager.setDefaultTitle("{{project_long_name}}");

// Add an ajax preprocessor to always have the csfr token
Ajax.addPreprocessor((options) => {
    options.credentials = options.credentials || "include";
    options.headers.set("X-CSRFToken", getCookie("csrftoken"));
});


GlobalState.registerStream = function (streamName) {
    WebsocketSubscriber.addListener(streamName, GlobalState.applyEventWrapper);
};

//Register on the global event stream
GlobalState.registerStream("global-events");

//Register on the user event stream
if (self.USER && self.USER.id) {
    GlobalState.registerStream("user-" + self.USER.id + "-events");
}
