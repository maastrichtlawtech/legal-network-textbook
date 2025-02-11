<template>
    <section id="presentation">
        <h3 id="university">MAASTRICHT UNIVERSITY</h3>
        <h3 id="lawtechlab">LAW AND TECH LAB</h3>
        <div id="title">
            <h1>{{ title }}</h1>
        </div>
        <div id="version">
            <h3>Version: {{ version }}</h3>
        </div>
        <div v-if="version && version < 1" id="donotcite">
            <h3>DO NOT CITE</h3>
        </div>
        <div id="authors">
            <h4 v-for="author in authors">
                {{ author }}
            </h4>
        </div>
        <div id="placeanddate">
            <h5>
                {{ place }}, {{ date }}
            </h5>
        </div>
    </section>
</template>
<script setup lang="ts">

const props = defineProps({
    title: String,
    version: Number,
    authors: Array<String>,
    place: String,
    date: String
});

</script>
<style scoped>

#presentation {
    text-align: center;
    padding: 50px;
    margin-bottom: 100px;
    border-bottom: solid 2px black;
}

#presentation > #university {
    margin-bottom: 40px;
}

#presentation > #title {
    border-top: 2px solid black;
    border-bottom: 2px solid black;
    margin: 80px 0;
}

#presentation > #authors {
    margin: 120px 0;
}
</style>