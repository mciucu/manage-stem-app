import {UI, TabArea, Panel, Button} from "UI";

export class IndexPage extends UI.Element {
    render() {
        return [
            <TabArea>
                <Panel title="First">
                    <h1>${author}$</h1>
                </Panel>
                <Panel title="Second">
                    <h2>The second panel</h2>
                    <Button>Push me!</Button>
                </Panel>
            </TabArea>
        ]
    }
}
