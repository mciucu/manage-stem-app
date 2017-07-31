import {UI, ViewportMeta} from "UI";
import {MAIN_ROUTE} from "./Routes"
import {Navbar} from "./Navbar";
import {StemApp} from "app/StemApp";

import {MAIN_ROUTE} from "./Routes";

export class AppClass extends StemApp {
    getBeforeContainer() {
        return <Navbar ref="navbar"/>;
    }

    getRoutes() {
        return MAIN_ROUTE;
    }
}