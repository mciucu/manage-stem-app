import {UI} from "UI";
import {MAIN_ROUTE} from "./Routes"
import {AppNavManager} from "./AppNavManager.jsx";
import {EstablishmentApp} from "EstablishmentApp";

export class AppClass extends EstablishmentApp {
    getBeforeContainer() {
        return <AppNavManager ref="navManager"/>;
    }

    getRoutes() {
        return MAIN_ROUTE;
    }
}
