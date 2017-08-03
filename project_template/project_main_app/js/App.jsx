import {UI, ViewportMeta} from "UI";
import {MAIN_ROUTE} from "./Routes"
import {AppNavManager} from "./AppNavManager.jsx";
import {StemApp} from "app/StemApp";

export class AppClass extends StemApp {
    getBeforeContainer() {
        return <AppNavManager ref="navManager"/>;
    }

    getRoutes() {
        return MAIN_ROUTE;
    }
}
