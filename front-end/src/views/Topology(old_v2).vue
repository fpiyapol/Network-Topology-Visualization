<template>
    <div
        id="topology"
        :class="{'deactive':!isActive}"
    >
        <HamburgerButton />
        <v-stage
            ref="stage"
            :config="configKonva"
            @dragstart="handleDragstart"
            @dragend="handleDragend"
            @dragmove="handleDragMove"
        >
            <v-layer ref="lineLayer">
                <v-line
                    v-for="(link, index) in allLinks"
                    :key="index"
                    :config="link"
                >
                </v-line>
            </v-layer>
            <v-layer>
                <v-text
                    v-for="(hostname, index) in allHostLabel"
                    :key="index"
                    :config="hostname"
                ></v-text>
            </v-layer>
            <v-layer ref="nodeLayer">
                <v-circle
                    v-for="(circle, index) in circles"
                    :key="index"
                    :config="circle"
                ></v-circle>
            </v-layer>
            <v-layer ref="dragLayer"></v-layer>
        </v-stage>
    </div>
</template>

<script>
import { mapState } from "vuex";
import { EventBus } from "../main.js";
import HamburgerButton from "../components/Hamburger.vue";

let vm = {};
export default {
    name: "Topology",
    data() {
        return {
            isActive: true,
            configKonva: {
                width: 0,
                height: 0
            },
            circles: [],
            setting: {
                hostnameLabel: true
            },
            allNodeDevice:[],
            ud: null
        };
    },
    computed: {
        ...mapState(["devices"]),
        allLinks() {
            let arrLink = []; // this array (is tmp array) keep all links (edge)
            for (let l in this.$store.state.links) {
                let point = [];
                for (let c in this.circles) {
                    if (
                        this.circles[c].name ==
                        this.$store.state.links[l].coord1
                    ) {
                        point.push(this.circles[c].x);
                        point.push(this.circles[c].y);
                    } else if (
                        this.circles[c].name ==
                        this.$store.state.links[l].coord2
                    ) {
                        point.push(this.circles[c].x);
                        point.push(this.circles[c].y);
                    }
                }
                if (point.length == 4) {
                    arrLink.push({
                        points: point,
                        stroke: "white"
                    });
                }
            }
            return arrLink;
        },
        allHostLabel() {
            let arr = [];
            if (this.setting.hostnameLabel) {
                this.circles.forEach(element => {
                    let strLength = element.name.length / 2 + 1;
                    arr.push({
                        x: element.x - strLength * 5,
                        y: element.y + 40,
                        text: element.name,
                        fill: "white"
                    });
                });
            }
            return arr;
        }
    },
    beforeDestroy() {
        clearInterval(this.ud);
    },
    created() {
        // this.update();
    },
    methods: {
        update() {
            this.ud = setInterval(() => {
                this.circles.forEach(element => {
                    console.log(element.name)
                })
            }, 3000);
        },
        stageResize() {
            // when window size change then resize (Konva)stage.
            setTimeout(() => {
                this.configKonva.width = this.$el.clientWidth;
                this.configKonva.height = this.$el.clientHeight;
                this.$refs.stage.getStage().draw();
            }, 1000);
        },
        handleDragstart(e) {
            const shape = e.target;
            const dragLayer = vm.$refs.dragLayer.getNode();
            const stage = vm.$refs.stage.getNode();
            // moving to another layer will improve dragging performance - Konva.
            shape.moveTo(dragLayer);
            stage.draw();
        },
        handleDragend(e) {
            const shape = e.target;
            const layer = vm.$refs.nodeLayer.getNode();
            const stage = vm.$refs.stage.getNode();
            shape.moveTo(layer);
            stage.draw();
            for (let c in this.circles) {
                if (this.circles[c].name == shape.attrs.name) {
                    this.circles[c].x = shape.attrs.x;
                    this.circles[c].y = shape.attrs.y;
                }
            }
        },
        handleDragMove(e) {
            const shape = e.target;
            const dragLayer = vm.$refs.dragLayer.getNode();
            const stage = vm.$refs.stage.getNode();
            // moving to another layer will improve dragging performance - Konva
            shape.moveTo(dragLayer);
            stage.draw();
            for (let c in this.circles) {
                if (this.circles[c].name == shape.attrs.name) {
                    this.circles[c].x = shape.attrs.x;
                    this.circles[c].y = shape.attrs.y;
                }
            }
        }
    },
    mounted() {
        vm = this;

        this.configKonva.width = this.$el.clientWidth;
        this.configKonva.height = this.$el.clientHeight;

        // this.$store.dispatch("loadDevices");
        this.$store.dispatch("loadNodeLinks");

        EventBus.$on("clicked", data => {
            this.isActive = data;
            this.stageResize();
        });



        let width = this.configKonva.width;
        let height = this.configKonva.height;
        // define width & height for positioning node

        let allDevices = this.$store.state.devices;
        let adIndex = 0;
        // adIndex - allDevicesIndex (index for array)
        let allNodes = this.$store.state.devices.length;
        let lines = (allNodes % 2) + Math.floor(allNodes / 2);
        //lines - calculate number of line(s).

        if (allNodes % 2 == 1) {
            // Check even/odd node (actually check odd)
            //     *    <-- display this odd node first
            //   *   *
            // and the other lines have 2 nodes per line.
            this.circles.push({
                name: allDevices[adIndex].hostname,
                ip_addr: allDevices[adIndex].ip_addr,
                x: width / 2,
                y: height / (lines + 1),
                fillLinearGradientStartPoint: { x: -30, y: -30 },
                fillLinearGradientEndPoint: { x: 30, y: 30 },
                fillLinearGradientColorStops: [
                    0,
                    "#89764c",
                    0.5,
                    "#c4af73",
                    1,
                    "#89764c"
                ],
                radius: 33,
                draggable: true,
                shadowColor: "black",
                shadowBlur: 10,
                shadowOffsetX: 5,
                shadowOffsetY: 5,
                shadowOpacity: 0.6
            });
            lines--;
            adIndex++;
        }
        for (
            let line = -Math.floor(lines / 2);
            line <= Math.floor((lines - 1) / 2);
            line++
        ) {
            for (let i = 1; i >= 0; i--) {
                this.circles.push({
                    name: allDevices[adIndex].hostname,
                    ip_addr: allDevices[adIndex].ip_addr,
                    x: Math.abs(
                        width * i -
                            width /
                                (2.5 + Math.floor(lines / 2) - Math.abs(line))
                    ),
                    y: Math.abs(
                        (line > 0 ? height : 0) - height / (2 + Math.abs(line))
                    ),
                    fillLinearGradientStartPoint: { x: -30, y: -30 },
                    fillLinearGradientEndPoint: { x: 30, y: 30 },
                    fillLinearGradientColorStops: [
                        0,
                        "#89764c",
                        0.5,
                        "#c4af73",
                        1,
                        "#89764c"
                    ],
                    radius: 30,
                    draggable: true,
                    shadowColor: "black",
                    shadowBlur: 10,
                    shadowOffsetX: 5,
                    shadowOffsetY: 5,
                    shadowOpacity: 0.6
                });
                adIndex++;
            }
        }
    },
    components: {
        HamburgerButton
    }
};
</script>

<style scoped>
#topology {
    background: linear-gradient(135deg, hsl(0, 0%, 18%), hsl(0, 0%, 2%));
    /* background: linear-gradient(135deg, hsl(46, 33%, 30%), hsl(45, 30%, 18%), hsl(0, 0%, 10%), hsl(0, 0%, 2%)); */
    overflow: hidden;
    width: 83.33%;
    transition: width 1.2s;
    position: relative;
}
.deactive {
    /* Sidebar - deactive */
    width: 100% !important;
    transition: width 1.2s;
}
</style>