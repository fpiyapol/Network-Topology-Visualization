<template>
    <div
        id="main-board"
        :class="{'deactive':!isActive}"
    >
        <HamburgerButton />
        <Toasts/>
        <b-button
            v-show="devices.length > 0"
            id="circle-add-btn"
            @click="show=true"
        >+</b-button>
        <div
            id="main-panel"
            class="w-100 h-100 pt-5 pl-5"
        >
            <div
                id="announcement"
                v-show="devices.length == 0"
            >
                <h2>There is no device available, please</h2>
                <b-button
                    @click="show=true"
                    id="add-btn"
                >add device</b-button>
            </div>

            <transition-group
                name="fade"
                style="display:flex; flex-wrap:wrap; height:0"
            >
                <div
                    v-show="devices.length > 0"
                    v-for="(device, index) in devices"
                    :key="index"
                >
                    <b-card class="m-3">
                        <b-card-text>
                            <h3>
                                {{device.hostname}}
                            </h3>
                            <!-- <div class="card-sep">
                                <p>
                                    IP : {{device.ip_addr}}
                                </p>
                            </div> -->
                        </b-card-text>
                    </b-card>
                </div>
            </transition-group>
            <b-modal
                v-model="show"
                id="modal"
                title="ADD DEVICE"
            >
                <b-form>
                    <label for="ip-addr">IP Address : </label>
                    <b-form-input
                        id="ip-addr"
                        required
                        placeholder="IP Address"
                        v-model="ip_addr"
                    ></b-form-input>
                </b-form>
                <b-form>
                    <label for="username">Username : </label>
                    <b-form-input
                        id="username"
                        required
                        placeholder="Username"
                        v-model="username"
                    ></b-form-input>
                </b-form>
                <b-form>
                    <label for="password">Password : </label>
                    <b-form-input
                        id="password"
                        required
                        type="password"
                        placeholder="Password"
                        v-model="password"
                    ></b-form-input>
                </b-form>
                <b-form>
                    <label for="en-pass">Enable Password : </label>
                    <b-form-input
                        id="en-pass"
                        required
                        type="password"
                        placeholder="Enable Password"
                        v-model="enpass"
                    ></b-form-input>
                </b-form>
                <div
                    slot="modal-footer"
                    class="w-100"
                >
                    <b-button
                        class="float-right btn-modal"
                        @click="show=false"
                    >
                        cancel
                    </b-button>
                    <b-button
                        id="submit-btn"
                        class="float-right btn-modal"
                        @click="show=false; addDevice()"
                    >
                        submit
                    </b-button>
                </div>
            </b-modal>
        </div>
    </div>
</template>

<script>
import { EventBus } from "../main.js";
import { mapState, mapActions } from "vuex";
import HamburgerButton from "../components/Hamburger.vue";
import Toasts from "../components/Toasts.vue"
export default {
    name: "Home",
    data() {
        return {
            show: false,
            isActive: true,
            ip_addr: "",
            username: "",
            password: "",
            enpass: ""
        };
    },
    mounted() {
        EventBus.$on("clicked", data => {
            this.isActive = data;
        });
    },
    methods: {
        addDevice() {
            let payload = {
                ip_addr: this.ip_addr,
                username: this.username,
                password: this.password,
                enpass: this.enpass
            };
            this.$store.dispatch("addDevice", payload);
            this.ip_addr = "";
            this.username = "";
            this.password = "";
            this.enpass = "";
        }
    },
    computed: {
        ...mapState(["devices"]),
        payload() {
            return {
                device: {
                    ip_addr: this.ip_addr,
                    username: this.username,
                    password: this.password,
                    enpass: this.enpass
                }
            };
        }
    },
    components: {
        HamburgerButton,
        Toasts
    }
};
</script>

<style scoped>
#main-board {
    position: relative;
    background: linear-gradient(135deg, hsl(0, 0%, 18%), hsl(0, 0%, 2%));
    padding: 0;
    width: 83.33%;
    transition: width 1.2s;
    color: white;
}

.deactive {
    /* Sidebar - deactive */
    width: 100% !important;
    transition: width 1.2s;
}

#main-panel {
    display: flex;
}
#announcement {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}
#add-btn {
    background: hsl(0, 0%, 8%);
    border: solid #c4af73;
    border-width: 1px;
    margin-top: 0.55vh;
}
#add-btn:focus {
    box-shadow: none;
}
.card {
    width: 15vw;
    min-width: 15vw;
    background: #262626;
    border: 1.5px solid #c4af73;
    text-align: center;
    box-shadow: 0 4px 8px 2px rgba(0, 0, 0, 0.6);
    border-radius: 0;
    font-size: 1em;
}
.card-body {
    padding: 20px 0;
}
.card-sep {
    background: #212121;
    padding: 5%;
}
.card-sep p {
    margin: 0;
}
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.5s;
}
.fade-enter,
.fade-leave-to {
    opacity: 0;
}
#cards {
    display: flex;
}
#circle-add-btn {
    width: 50px;
    height: 50px;
    background-image: linear-gradient(
        -30deg,
        hsl(45, 35%, 40%),
        hsl(45, 35%, 60%),
        hsl(45, 35%, 40%)
    );
    border-radius: 50%;
    position: absolute;
    right: 4%;
    bottom: 4%;
}
#circle-add-btn:focus {
    box-shadow: none;
}
</style>

<style>
.modal-header,
.modal-body,
.modal-content,
.modal-footer {
    background: hsl(0, 0%, 15%);
    text-align: left;
}
.modal-header {
    border-bottom: 1px solid #c4af73;
}
.modal-footer {
    border-top: 1px solid #c4af73;
}
.close {
    color: white;
}
form {
    margin: 2% 0;
}
.btn-modal {
    margin: 0 2%;
}
</style>
