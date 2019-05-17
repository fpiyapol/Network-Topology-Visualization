<template>
    <div
        id="side-navbar"
        :class="{deactive:!isActive}"
    >
        <transition name="fade">
            <div
                class="menu-list"
                v-show="isActive"
            >
                <div
                    id="menu-header"
                    class="menu-item"
                >
                    <h4>
                        NTV
                    </h4>
                </div>
                <b-link to="/">
                    <div class="menu-item">
                        <img
                            src="../assets/home.svg"
                            alt="control-panel"
                        >
                        <p>Home</p>

                    </div>
                </b-link>
                <!-- <b-link to="/">
                    <div class="menu-item">
                        <img
                            src="../assets/control-panel.svg"
                            alt="control-panel"
                        >
                        <p>Dashboard</p>

                    </div>
                </b-link> -->
                <b-link to="/topology">
                    <div class="menu-item">
                        <img
                            src="../assets/topology.svg"
                            alt="topology"
                        >
                        <p>Topology</p>
                    </div>
                </b-link>
            </div>
        </transition>
    </div>
</template>

<script>
import { EventBus } from "../main.js";
export default {
    name: "SideNavbar",
    data() {
        return {
            isActive: true
        };
    },
    mounted() {
        EventBus.$on("clicked", data => {
            this.isActive = data;
        });
    }
};
</script>

<style scoped>
#side-navbar {
    background: hsl(0, 0%, 8%);
    padding: 0;
    display: flex;
    flex-direction: column;
    width: 16.67%;
    transition: width 1.2s;
}

.deactive {
    width: 0% !important;
    transition: width 1.2s;
}

img {
    width: 2em;
    height: auto;
    margin: 0 5%;
}

p {
    color: white;
    font-size: 1em;
    margin: 0;
}

#menu-header {
    width: 100%;
    text-align: center;
    padding: 1% 0;
    color: #c4af73;
    justify-content: center;
    align-items: center;
    border: none;
    cursor: default;
}

h4 {
    margin: 0;
}

.menu-item {
    width: 100%;
    display: flex;
    align-items: center;
    border: solid hsl(0, 0%, 8%) 1px;
    padding: 0.6em 0;
}

a {
    text-decoration: none;
}

.menu-item:hover {
    border: solid #c4af73 1px;
    cursor: pointer;
}

.fade-leave-active {
    transition: opacity 0.5s;
}

.fade-enter-active {
    transition: opacity 0.5s;
    transition-delay: 0.3s;
}

.fade-enter,
.fade-leave-to {
    opacity: 0;
}
</style>
