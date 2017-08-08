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
import {LoginModal} from "LoginModal";

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
                    margin: "0",
                    // paddingLeft: this.leftSidePanel ? "0px" : "50px",
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
                    margin: "0",
                    // paddingRight: this.rightSidePanel ? "0px" : "50px",
                }}>
                {
                    /*!USER.isAuthenticated &&*/
                    <NavElement value="Login/Signup" onClick={() => LoginModal.show()} />
                }
            </NavSection>
        ];
    }
}


export {AppNavManager};