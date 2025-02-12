<template>
    <main>
        <!-- LEFT COLUMN (INDEX AND CONTROLS) -->
        <TableOfContents :tocItems="tocItems" />
        <section id="notebooks-container">
            <!-- PRESENTATION PAGE -->
            <Presentation v-if="presentation" :university="presentation.university" :department="presentation.department"
                :title="presentation.title" :version="presentation.version" :authors="presentation.authors"
                :place="presentation.place" :date="presentation.date" />
            <!-- NOTEBOOKS CONTENT -->
            <div v-for="nb in notebooks">
                <div v-html="nb"></div>
            </div>
        </section>
    </main>
</template>
<script setup lang="ts">
import { onMounted, ref } from "vue";
import Presentation from "./Presentation.vue";
import TableOfContents from "./TableOfContents.vue";
import "https://cdn.jsdelivr.net/npm/ipynb2html@0.4.0-rc.1/dist/ipynb2html-full.min.js";

declare let ipynb2html: any;

const config = ref();
const notebooks = ref<string[]>([]);
const presentation = ref<{
    university: String,
    department: String,
    title: String,
    version: Number,
    authors: Array<String>,
    place: String,
    date: String
}>();

const tocItems = ref<{ label: string, url: string }[][]>([]);

const loadNotebooks = async () => {
    const configFile = await fetch('/nbconfig.json');
    config.value = await configFile.json();
    presentation.value = config.value.presentation;
    const notebooksNames = config.value.notebooks;
    for (let i = 0; i < notebooksNames.length; ++i) {
        const nb: string = notebooksNames[i];
        const file = await fetch(`/notebooks/${nb}.ipynb`);
        var json = await file.json();
        var rendered = ipynb2html.render(json);
        addToToc(rendered);
        notebooks.value.push(rendered.outerHTML);
    }
};

const addToToc = (node: HTMLElement) => {

    if (node.tagName == 'H1') {
        tocItems.value.push([{ label: node.innerText, url: getUrl(node) }]);
    } else if (node.tagName == 'H2') {
        tocItems.value.at(-1).push({ label: node.innerText, url: getUrl(node) });
    }

    //TODO: upgrade for h3

    let child = node.firstChild;
    while (child) {
        addToToc(child as HTMLElement);
        child = child.nextSibling;
    }
};

function getUrl(node: HTMLElement) {
    let url = node.innerText.toLowerCase();
    url = url.replaceAll(/[^a-zA-Z0-9\s-]/g, '');
    url = url.replaceAll(' ', '-');
    return url;
}


onMounted(async () => {
    await loadNotebooks();
})
</script>
<style>
@import url('https://cdn.jsdelivr.net/npm/ipynb2html@0.4.0-rc.1/dist/notebook.min.css');
@import url('https://cdn.jsdelivr.net/npm/katex@0.16.3/dist/katex.min.css');
@import url('https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@10.7.3/build/styles/default.min.css');

#notebooks-container {
    position: relative;
    overflow: auto;
    padding: 0 20px;
    font-family: Georgia, "Times New Roman", Times, serif;
}

#notebooks-container * code {
    white-space: pre-wrap;
}

#notebooks-container * p {
    overflow-x: auto;
}

#notebooks-container * img {
    display: block;
    margin-left: auto;
    margin-right: auto;
    max-width: 100%;
}

#notebooks-container * .nb-input::before {
    display: contents !important;
}

#notebooks-container * .nb-output::before {
    display: contents !important;
}
</style>
