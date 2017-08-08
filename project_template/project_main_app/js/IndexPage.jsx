import {UI, Link, registerStyle} from "UI";
import {Card} from "./Card";
import {IndexPageStyle, QuoteStyle, CodeStyle} from "./IndexPageStyle";

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
