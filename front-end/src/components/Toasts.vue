<template>
    <transition name="fade">
        <div
            id="toasts"
            class="shadow"
            v-show="show"
        >

            <div id="t-header">Notification</div>
            <div id="t-content">Topology has changed.</div>
        </div>
    </transition>
</template>

<script>
import { EventBus } from "../main.js";
export default {
    name: "Toasts",
    data() {
        return {
            show: false
        };
    },
    mounted() {
        EventBus.$on("noti", data => {
            this.show = data;
            setTimeout(() => this.show = false, 3500)
        });
    }
};
</script>

<style scoped>
#toasts {
    position: absolute;
    width: 20%;
    height: 15%;
    background: rgba(68, 68, 68, 0.97);
    top: 2%;
    right: 1%;
    z-index: 2;
    border-radius: 2%;
}
#t-header {
    width: 100%;
    height: 30%;
    padding-left: 5%;
    background: #222;
    color: #c4af73;
    text-align: left;
    align-items: center;
    display: flex;
}
#t-content {
    width: 100%;
    height: 70%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
}
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
    opacity: 0;
}
</style>
