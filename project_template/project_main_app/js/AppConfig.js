import {UI, CodeEditor} from "UI";

import {Ajax} from "base/Ajax";
import {ensure} from "base/Require";
import {getCookie} from "base/Utils";

import {GlobalState} from "state/State";

import {WebsocketSubscriber} from "websocket/WebsocketSubscriber";

// Add an ajax preprocessor to always have the csfr token
Ajax.addDefaultPreprocessor((options) => {
    options.credentials = options.credentials || "include";
    options.headers.set("X-CSRFToken", getCookie("csrftoken"));
});

CodeEditor.requireAce = function (callback) {
    ensure(["/static/js/ext/ace/ace.js"], callback);
};

GlobalState.registerStream = function (streamName) {
    WebsocketSubscriber.addListener(streamName, GlobalState.applyEventWrapper);
};

//Register on the global event stream
GlobalState.registerStream("global-events");

//Register on the user event stream
if (self.USER && self.USER.id) {
    GlobalState.registerStream("user-" + self.USER.id + "-events");
}
