import {UI, registerStyle} from "UI";
import {CardStyle} from "./CardStyle";


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