<template>
    <img
        src="../assets/hamburger.svg"
        alt=""
        @click="onClick()"
    >
</template>

<script>
import { EventBus } from "../main.js";
export default {
    name: "HamburgerButton",
    data(){
        return{
            isActive: true
        }
    },
    methods:{
        onClick(){
            this.isActive = !this.isActive;
            EventBus.$emit("clicked", this.isActive);
        }
    }
};
</script>

<style scoped>
img {
    left: 0;
    margin: 1%;
    width: 1.5em;
    height: auto;
    cursor: pointer;
    z-index: 10;
    position: absolute;
}
</style>


