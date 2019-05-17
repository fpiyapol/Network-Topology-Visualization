import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        devices: [],
        links: []
    },
    mutations: {
        setDevices(state, devices) {
            state.devices = devices.devices;
        },
        setNodeLinks(state, links) {
            state.links = links.links;
        }
    },
    actions: {
        // https://api.myjson.com/bins/qzse4 --> https://api.myjson.com/bins/sda10
        // https://api.myjson.com/bins/177jwg --> https://api.myjson.com/bins/whr0g
        // https://api.myjson.com/bins/1631kg --> https://api.myjson.com/bins/1d88ts six devices
        // https://api.myjson.com/bins/1fljtc --> no device
        // https://api.myjson.com/bins/18jt3m
        // https://api.myjson.com/bins/j58pu
        // http://localhost:5000/api/devices/
        loadDevices({ commit }) {
            axios({
                method: "get",
                url: "http://localhost:5000/api/devices/"
            })
                .then(r => r.data)
                .then(devices => {
                    commit("setDevices", devices);
                });
        },
        // https://api.myjson.com/bins/ have
        updateDevices({commit}){
            axios({
                method: "get",
                url: "http://localhost:5000/api/update/"
            })
                .then(r => r.data)
                .then(devices => {
                    commit("setDevices", devices);
                });
        },
        addDevice({ commit }, payload) {
            axios({
                method: "post",
                url: "http://127.0.0.1:5000/api/devices/",
                data: {
                    device: {
                        ip_addr: payload.ip_addr,
                        username: payload.username,
                        password: payload.password,
                        en_pass: payload.enpass
                    }
                }
            });
        }
    }
});
