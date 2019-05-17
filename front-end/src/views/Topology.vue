<template>
    <div
        id="topology"
        :class="{'deactive':!isActive}"
    >
        <HamburgerButton />
        <Toasts />
        <v-stage
            ref="stage"
            :config="configKonva"
            @dragstart="handleDragstart"
            @dragend="handleDragend"
            @dragmove="handleDragMove"
            @wheel="onWheel"
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
                <v-text
                    v-for="(intf, index) in allInterfaceLabel"
                    :key="index"
                    :config="intf"
                >
                </v-text>
            </v-layer>
            <v-layer ref="nodeLayer">
                <v-circle
                    v-for="(circle, index) in circles"
                    :key="index"
                    :config="circle"
                ></v-circle>
                <v-rect
                    v-for="(rect, index) in rects"
                    :key="index"
                    :config="rect"
                ></v-rect>
            </v-layer>
            <v-layer ref="dragLayer"></v-layer>
        </v-stage>
    </div>
</template>

<script>
import { mapState } from "vuex";
import { EventBus } from "../main.js";
import HamburgerButton from "../components/Hamburger.vue";
import Toasts from "../components/Toasts.vue";

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
            rects: [],
            setting: {
                hostnameLabel: true,
                interfaceLabel: true,
                hostnameFontSize: 14
            },
            allNodeDevice: [],
            ud: null
        };
    },
    computed: {
        ...mapState(["devices"]),
        allLinks() {
            let arrLink = []; // this array (is tmp array) keep all links (edge)
            let dest = [];
            let src = [];
            let intfSrc = "";
            let intfDest = "";
            this.allNodeDevice.forEach(node => {
                node.interfaces.forEach(intf => {
                    let point = [];
                    let data_1 = intf;
                    let thisNodeInterface = data_1.port;
                    let neighborHostname = data_1.n_hostname;
                    let neighborInterface = data_1.n_interface;
                    for (let n in this.allNodeDevice) {
                        let node2 = this.allNodeDevice[n];
                        for (let l in this.allNodeDevice[n].interfaces) {
                            let data_2 = node2.interfaces[l];
                            if (
                                neighborHostname == node2.name &&
                                neighborInterface == data_2.port &&
                                (!src.includes(node2.name) &&
                                    !dest.includes(node.name))
                            ) {
                                point.push(
                                    node.x + (node.device_type == "S" ? 25 : 0)
                                );
                                point.push(
                                    node.y +
                                        (node.device_type == "S" ? 22.5 : 0)
                                );
                                point.push(
                                    node2.x +
                                        (node2.device_type == "S" ? 25 : 0)
                                );
                                point.push(
                                    node2.y +
                                        (node2.device_type == "S" ? 22.5 : 0)
                                );
                                src.push(node.name);
                                dest.push(node2.name);
                                intfSrc = thisNodeInterface;
                                intfDest = data_2.port;
                                break;
                            }
                        }
                    }
                    if (point.length > 0) {
                        arrLink.push({
                            points: point,
                            stroke: "white",
                            src: intfSrc,
                            dst: intfDest
                        });
                    }
                });
            });
            return arrLink;
        },
        allHostLabel() {
            let arr = [];
            if (this.setting.hostnameLabel) {
                this.allNodeDevice.forEach(element => {
                    let text = element.device_type + ": " + element.name;
                    let strLength = text.length / 2 + 1;
                    arr.push({
                        x: element.x - (element.device_type == "R" ? strLength * 5 : (strLength * 5 > 35 ? strLength * 2.5 : 0)),
                        y: element.y + (element.device_type == "R" ? 40 : 65),
                        text: text,
                        fill: "white",
                        fontSize: this.setting.hostnameFontSize
                    });
                });
            }
            return arr;
        },
        allInterfaceLabel() {
            let intfLabel = [];
            let width = this.configKonva.width;
            let height = this.configKonva.height;
            if (this.setting.interfaceLabel) {
                this.allLinks.forEach(link => {
                    // let srcX = link.points[0] + (45 - Math.abs(link.points[1] - link.points[3]))
                    let srcX =
                        link.points[0] +
                        (link.points[0] < link.points[2] ? 50 : -45);
                    let srcY =
                        link.points[1] +
                        (link.points[1] >= height / 2 ? -20 : +20);
                    let dstX =
                        link.points[2] +
                        (link.points[2] < link.points[0] ? 50 : -50);
                    let dstY =
                        link.points[3] +
                        (link.points[3] >= height / 2 ? -20 : +20);
                    intfLabel.push({
                        x: srcX,
                        y: srcY,
                        text: link.src,
                        fill: "white"
                    });
                    intfLabel.push({
                        x: dstX,
                        y: dstY,
                        text: link.dst,
                        fill: "white"
                    });
                });
            }
            return intfLabel;
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
                    console.log(element.name);
                });
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
            for (let n in this.allNodeDevice) {
                if (
                    this.allNodeDevice[n].name == shape.attrs.name &&
                    this.allNodeDevice[n].interfaces[0] ==
                        shape.attrs.interfaces[0]
                ) {
                    this.allNodeDevice[n].x = shape.attrs.x;
                    this.allNodeDevice[n].y = shape.attrs.y;
                    break;
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

            for (let n in this.allNodeDevice) {
                if (
                    this.allNodeDevice[n].name == shape.attrs.name &&
                    this.allNodeDevice[n].interfaces[0] ==
                        shape.attrs.interfaces[0]
                ) {
                    this.allNodeDevice[n].x = shape.attrs.x;
                    this.allNodeDevice[n].y = shape.attrs.y;
                    break;
                }
            }
        },
        onWheel(e) {
            const stage = vm.$refs.stage.getNode();
            let scaleBy = 1.01;
            e.evt.preventDefault();
            let oldScale = stage.scaleX();
            let mousePointTo = {
                x:
                    stage.getPointerPosition().x / oldScale -
                    stage.x() / oldScale,
                y:
                    stage.getPointerPosition().y / oldScale -
                    stage.y() / oldScale
            };

            let newScale =
                e.evt.deltaY > 0 ? oldScale * scaleBy : oldScale / scaleBy;
            stage.scale({ x: newScale, y: newScale });

            var newPos = {
                x:
                    -(
                        mousePointTo.x -
                        stage.getPointerPosition().x / newScale
                    ) * newScale,
                y:
                    -(
                        mousePointTo.y -
                        stage.getPointerPosition().y / newScale
                    ) * newScale
            };
            stage.position(newPos);
            stage.batchDraw();
        }
    },
    mounted() {
        // this.$store.dispatch("loadNodeLinks");
        EventBus.$on("clicked", data => {
            this.isActive = data;
            this.stageResize();
        });
        this.$store.dispatch("loadDevices");
        vm = this;

        this.configKonva.width = this.$el.clientWidth;
        this.configKonva.height = this.$el.clientHeight;
        //set konva stage width and height

        setTimeout(() => {
            let width = this.configKonva.width;
            let height = this.configKonva.height;
            // define width & height for positioning node --> (node is device (router and switch))

            let allNodes = this.$store.state.devices;
            let adIndex = 0;
            // adIndex --> allNodesIndex (index for (allNodes) array)
            let numberOfNodes = allNodes.length;
            let lines = (numberOfNodes % 2) + Math.floor(numberOfNodes / 2);
            //lines - calculate number of line(s).

            if (numberOfNodes % 2 == 1) {
                // Check even/odd node (actually check odd)
                //     *    <-- display this odd node first
                //   *   *
                // and the other lines have 2 nodes per line.
                if (allNodes[adIndex].device_type == "R") {
                    this.circles.push({
                        name: allNodes[adIndex].hostname,
                        device_type: allNodes[adIndex].device_type,
                        interfaces: allNodes[adIndex].interfaces,
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
                } else {
                    this.rects.push({
                        name: allNodes[adIndex].hostname,
                        device_type: allNodes[adIndex].device_type,
                        interfaces: allNodes[adIndex].interfaces,
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
                        width: 60,
                        height: 60,
                        draggable: true,
                        shadowColor: "black",
                        shadowBlur: 10,
                        shadowOffsetX: 5,
                        shadowOffsetY: 5,
                        shadowOpacity: 0.6
                    });
                }
                lines--;
                adIndex++;
            }
            for (
                let line = -Math.floor(lines / 2);
                line <= Math.floor((lines - 1) / 2);
                line++
            ) {
                for (let i = 0; i <= 1; i++) {
                    if (allNodes[adIndex].device_type == "R") {
                        this.circles.push({
                            name: allNodes[adIndex].hostname,
                            device_type: allNodes[adIndex].device_type,
                            interfaces: allNodes[adIndex].interfaces,
                            x: Math.abs(
                                width * i -
                                    width /
                                        (2.5 +
                                            Math.floor(lines / 2) -
                                            Math.abs(line))
                            ),
                            y: Math.abs(
                                (line > 0 ? height : 0) -
                                    height / (2 + Math.abs(line))
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
                    } else {
                        this.rects.push({
                            name: allNodes[adIndex].hostname,
                            device_type: allNodes[adIndex].device_type,
                            interfaces: allNodes[adIndex].interfaces,
                            x: Math.abs(
                                width * i -
                                    width /
                                        (2.5 +
                                            Math.floor(lines / 2) -
                                            Math.abs(line))
                            ),
                            y: Math.abs(
                                (line > 0 ? height : 0) -
                                    height / (2 + Math.abs(line))
                            ) - 22.5,
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
                            width: 55,
                            height: 55,
                            draggable: true,
                            shadowColor: "black",
                            shadowBlur: 10,
                            shadowOffsetX: 5,
                            shadowOffsetY: 5,
                            shadowOpacity: 0.6
                        });
                    }
                    adIndex++;
                }
            }
            this.allNodeDevice = this.circles.concat(this.rects);
        }, 500);
    },
    components: {
        HamburgerButton,
        Toasts
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