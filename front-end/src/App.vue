<template>
    <b-container
        fluid
        id="app"
        class="vh-100"
    >
        <b-row class="h-100">
            <SideNavbar />
            <router-view></router-view>
        </b-row>
    </b-container>
</template>

<script>
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";
import SideNavbar from "@/components/SideNavbar";
import { mapState, mapActions } from "vuex";
import { EventBus } from "./main";

export default {
    name: "app",
    components: { SideNavbar },
    data() {
        return {
            oldData: null
        };
    },
    mounted() {
        this.$store.dispatch("loadDevices");
        this.oldData = this.$store.state.devices;
        setInterval(() => {
            this.$store.dispatch("updateDevices");
            let newData = this.$store.state.devices;
            // console.log(JSON.stringify(this.oldData), JSON.stringify(newData))
            console.log(
                !(JSON.stringify(this.oldData) === JSON.stringify(newData))
            );
            if (!(JSON.stringify(this.oldData) === JSON.stringify(newData))) {
                console.log("changed");
                EventBus.$emit("noti", true);
                this.oldData = newData;
            }
        }, 5000);
    }
};
</script>


<style>
#app {
    font-family: "Avenir", Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
}
</style>
