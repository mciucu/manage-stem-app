// UI components
import {UI} from "UI";
import {NavManager} from "navmanager/NavManager";
import {
    BasicOrientedElement,
    NavAnchoredNotifications,
    NavElement,
    NavLinkElement,
    NavSection,
    navSessionManager,
} from "navmanager/NavElement";
import {Direction, Orientation} from "UI";

/*
 * This is the NavManager file of your app.
 *
 * Note that the whole app is a single page app.
 * Follow the instructions below in order to customize your application.
 *
 * Enjoy coding!
 */

class AppNavManager extends NavManager {
    constructor(props) {
        super(props);

        this.leftSidePanel = null;
        this.rightSidePanel = null;
    }

    getLeftFixed() {
        return [
            <NavSection
                anchor={Direction.LEFT}
                style={{
                    margin: 0,
                }}>
                <NavLinkElement value="Home" href="/" />
                <NavLinkElement value="Blog" href="/blog" />
            </NavSection>
        ];
    }

    getRightFixed() {
        return [
            <NavSection
                anchor={Direction.RIGHT}
                style={{
                    margin: 0,
                }}>
                <NavElement value="First" />
                <NavElement value="Second" />
                <NavElement value="Third" />
            </NavSection>
        ];
    }
}


export {AppNavManager};