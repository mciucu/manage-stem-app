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
import {logout} from "Logout";
import {FAIcon} from "ui/FontAwesome";

/*
 * This is the NavManager file of your app.
 *
 * Note that the whole app is a single page app.
 * Follow the instructions below in order to customize your application.
 */

class AppNavManager extends NavManager {
    leftSidePanel = null;
    rightSidePanel = null;

    getLeftFixed() {
        return [
            <NavSection anchor={Direction.LEFT} style={{margin: 0}}>
                <NavLinkElement value="Home" href="/" />
                <NavLinkElement value="Blog" href="/blog" />
            </NavSection>
        ];
    }

    getUserElement() {
        if (USER.isAuthenticated) {
            return <NavElement value={[<FAIcon icon="user" style={{marginRight: "0.3rem"}} />, USER.email]}>
                <NavElement value={UI.T("Settings")} />
                <NavElement value={UI.T("Logout")} onClick={() => logout()}/>
            </NavElement>;
        } else {
            return <NavElement value={UI.T("Login/Signup")} onClick={() => LoginModal.show()} />;
        }
    }

    getRightFixed() {
        return [
            <NavSection anchor={Direction.RIGHT} style={{margin: 0}}>
                {this.getUserElement()}
            </NavSection>
        ];
    }
}


export {AppNavManager};
