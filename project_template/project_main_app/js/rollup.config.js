import babel from 'rollup-plugin-babel';
import uglify from 'rollup-plugin-uglify';
import includePaths from "rollup-plugin-includepaths";

var fs = require("fs");
var path = require('path');

var rootDir = __dirname;

while (!fs.existsSynch(rootDir + "/stemapp.json")) {
    rootDir = path.dirname(rootDir);
    if (rootDir === path.dirname(rootDir)) {
        exit("Can't find stemapp.json in the path tree.");
    }
}

rootDir = path.normalize(rootDir + "/");

let establishmentModules = ["accounts", "blog", "chat", "content", "documentation", "errors", "forum", "localization"];
let modules = ["analytics", "{{project_main_app}}"];
for (let module of establishmentModules) {
    modules.push("establishment/" + module);
}

let modulesDirectories = [
    path.join(rootDir, "node_modules/stem-core/src/"),
    path.join(rootDir, "node_modules/stem-core/src/base"),
    path.join(rootDir, "node_modules/stem-core/src/data-structures"),
    path.join(rootDir, "node_modules/stem-core/src/markup"),
    path.join(rootDir, "node_modules/stem-core/src/state"),
    path.join(rootDir, "node_modules/stem-core/src/ui"),
    path.join(rootDir, "node_modules/stem-core/src/time"),
    path.join(rootDir, "node_modules/stem-core/src/ui/tabs"),
];

for (let module of modules) {
    modulesDirectories.push(path.join(rootDir, module, "/static/js"));
    modulesDirectories.push(path.join(rootDir, module, "/static/js/state"));
}

modulesDirectories.push(path.join(rootDir, "establishment/content/static/js/markup"));

let includePathOptions = {
    paths: modulesDirectories,
    external: ["d3"],
    extensions: [".es6.js", ".jsx", ".js"],
};


export default {
    entry: "Bundle.es6.js",
    format: "umd",
    moduleId: "bundle",
    moduleName: "bundle",
    plugins: [
        includePaths(includePathOptions),
        babel(),
        // uglify(),
    ],
    dest: "static/js/bundle.js"
};
