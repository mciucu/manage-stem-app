import {UI} from "UI";
import {StyleSheet, styleRule} from "UI";

export class CardStyle extends StyleSheet {
    @styleRule
    container = {
        width: "450px",
        maxHeight: "100%",
        maxWidth: "100%",

        backgroundColor: "#fff",
        boxShadow: "#a05100 0px 0px 10px",
    };

    @styleRule
    header = {
        height: "100px",
        width: "100%",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        fontSize: "28px",
    };

    @styleRule
    body = {
        paddingLeft: "20px",
        paddingRight: "20px",
        paddingBottom: "40px",
        textAlign: "center",
        fontSize: "17px",
        ">p": {
            margin: "0px",
        }
    };
}
