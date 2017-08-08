import {UI} from "UI";
import {StyleSheet, styleRule} from "UI";

export class IndexPageStyle extends StyleSheet {
    @styleRule
    container = {
        height: "100%",
        width: "100%",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        flexDirection: "column",
    };

    @styleRule
    topContainer = {
        flexGrow: "1.5",
        width: "100%",
        backgroundColor: "#f0a150",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
    };

    @styleRule
    bottomContainer = {
        flexGrow: "2",
        width: "100%",
        fontSize: "18px",
        paddingTop: "20px",
        textAlign: "center",
    };
}

export class QuoteStyle extends StyleSheet {
    @styleRule
    quote = {
        color: "#aaa",
        fontStyle: "italic",
        fontSize: "17px",
        marginTop: "10px",
    };
}

export class CodeStyle extends StyleSheet {
    @styleRule
    code = {
        backgroundColor: "#eee",
        fontSize: "15px",
        padding: "2px 8px",
        borderRadius: "5px",
        fontFamily: '"Fira Mono", "DejaVu Sans Mono", Menlo, Consolas, "Liberation Mono", Monaco, "Lucida Console", monospace',
    };
}