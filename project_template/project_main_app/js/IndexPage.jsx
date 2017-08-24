import {UI, Link, registerStyle} from "UI";
import {StyleSheet, styleRule} from "UI";


class CardStyle extends StyleSheet {
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

class QuoteStyle extends StyleSheet {
    @styleRule
    quote = {
        color: "#aaa",
        fontStyle: "italic",
        fontSize: "17px",
        marginTop: "10px",
    };
}

class CodeStyle extends StyleSheet {
    @styleRule
    code = {
        backgroundColor: "#eee",
        fontSize: "15px",
        padding: "2px 8px",
        borderRadius: "5px",
        fontFamily: '"Fira Mono", "DejaVu Sans Mono", Menlo, Consolas, "Liberation Mono", Monaco, "Lucida Console", monospace',
    };
}

class IndexPageStyle extends StyleSheet {
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


@registerStyle(CardStyle)
export class Card extends UI.Element {
    extraNodeAttributes(attr) {
        attr.addClass(this.styleSheet.container);
    }

    render() {
        let {headerText, bodyText} = this.options;

        return [
            <div className={this.styleSheet.header}>
                {headerText}
            </div>,
            <div className={this.styleSheet.body}>
                {
                    bodyText.map((line) => {
                        return <p>{line}</p>;
                    })
                }
            </div>
        ];
    }
}

@registerStyle(QuoteStyle)
class Quote extends UI.Element {
    render() {
        let {text, hasQuotes} = this.options,
            message = text;
        if (hasQuotes) {
            message = "\"" + message + "\"";
        }

        return <div className={this.styleSheet.quote}>
            {message}
        </div>;
    }
}

@registerStyle(CodeStyle)
class Code extends UI.Primitive("span") {
    extraNodeAttributes(attr) {
        attr.addClass(this.styleSheet.code);
    }
}

@registerStyle(IndexPageStyle)
export class IndexPage extends UI.Element {
    extraNodeAttributes(attr) {
        attr.addClass(this.styleSheet.container);
    }

    render() {
        let headerText = "Welcome ${author}$!";
        let bodyText = [
            "This is the beginning of your stem project.",
            <Quote text="${project_name}$" />,
            <Quote text="${project_description}$" hasQuotes={true} />,
        ];

        return [
            <div className={this.styleSheet.topContainer}>
                <Card headerText={headerText} bodyText={bodyText} />
            </div>,
            <div className={this.styleSheet.bottomContainer}>
                <p>
                    Get started by editing <Code>${project_main_app}$/js/IndexPage.jsx</Code>
                </p>
                <p>
                    Save the code and just refresh the page.
                </p>
                <p>
                    You can also use Stem components, for example - <Code>TabArea</Code>, <Code>Panel</Code>, <Code>Button</Code>
                </p>
                <p>
                    Check the docs <Link href="https://stemjs.org/docs/">here</Link>.
                </p>
            </div>
        ];
    }
}
