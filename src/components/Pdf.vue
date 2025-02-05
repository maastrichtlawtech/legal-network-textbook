<template>
    <div id="pdf-container">
        <div v-for="nb in notebooks">
            <div v-html="nb"></div>
        </div>
    </div>
</template>
<script setup lang="ts">
import { onMounted, ref } from "vue";

declare let ipynb2html: any;
const notebooks = ref<string[]>([]);

const loadNotebooks = async () => {
    const configFile = await fetch('/nbconfig.json');
    const config = await configFile.json();
    const notebooksNames = config.notebooks;
    for(let i = 0; i < notebooksNames.length; ++i) {
        const nb: string = notebooksNames[i];
        const file = await fetch(`/notebooks/${nb}.ipynb`);
        var json = await file.json();
        var rendered = ipynb2html.render(json);
        notebooks.value.push(rendered.outerHTML);
    }
};

onMounted(async () => {
    await loadNotebooks();
})
</script>
<style scoped>

</style>
