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
        >
            <v-layer ref="lineLayer">
                <v-line
                    v-for="link in allLinks"
                    :key="link.id"
                    :config="link"
                >
                </v-line>
            </v-layer>
            <v-layer
                ref="layer"
                @beforeDraw="updateLine()"
            >
                <v-circle
                    v-for="circle in circles"
                    :key="circle.id"
                    :config="circle"
                >
                </v-circle>
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
            configKonva: {
                width: 0,
                height: 0
            },
            isActive: true
        };
    },
    computed: {
        ...mapState(["devices", "links"]),
        circles() {
            console.log("circle");
            let width = this.configKonva.width;
            let height = this.configKonva.height;
            // define width & height for positioning node
            let nodesArr = [];
            let allDevices = [];
            let adIndex = 0; // adIndex - allDevicesIndex (index no for array)
            let allNodes = this.devices.length;
            let lines = (allNodes % 2) + Math.floor(allNodes / 2); //lines - calculate number of line.

            for (let item in this.devices) {
                allDevices.push(this.devices[item].hostname);
            }
            if (allNodes % 2 == 1) {
                // Check even/odd node
                //     *    <-- display this odd node first
                //   *   *
                // and the other lines have 2 nodes per line.
                nodesArr.push({
                    name: allDevices[adIndex],
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
                    nodesArr.push({
                        name: allDevices[adIndex],
                        x: Math.abs(
                            width * i -
                                width /
                                    (3 + Math.floor(lines / 2) - Math.abs(line))
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

                    adIndex++;
                }
            }
            return nodesArr;
        },
        eachNodePoints() {
            let obj = {};
            console.log("each");
            for (let cir in this.circles) {
                obj[this.circles[cir].name] = {
                    x: this.circles[cir].x,
                    y: this.circles[cir].y
                };
            }
            return obj;
        },
        allLinks() {
            console.log("allLinks");
            let allLinks = [];
            let p = [];
            // for (let l in this.links) {
            //     for (let c in this.circles) {
            //         if (this.circles[c].name == this.links[l].coor1) {
            //             p.push(this.circles[c].x);
            //             p.push(this.circles[c].y);
            //             for (let c2 in this.circles) {
            //                 if (this.circles[c2].name == this.links[l].coor2) {
            //                     p.push(this.circles[c2].x);
            //                     p.push(this.circles[c2].y);
            //                 }
            //             }
            //         }
            //     }
            //     allLinks.push({
            //         points: p,
            //         stroke: "white"
            //     });
            //     p = [];
            // }
            for (let o in this.eachNodePoints) {
                for (let l in this.links) {
                    p.push(this.eachNodePoints[this.links[l].coor1].x);
                    p.push(this.eachNodePoints[this.links[l].coor1].y);
                    p.push(this.eachNodePoints[this.links[l].coor2].x);
                    p.push(this.eachNodePoints[this.links[l].coor2].y);
                    allLinks.push({
                        points: p,
                        stroke: "white"
                    });
                }
                break;
            }
            return allLinks;
        }
    },
    methods: {
        stageResize() {
            setTimeout(() => {
                this.configKonva.width = this.$el.clientWidth;
                this.configKonva.height = this.$el.clientHeight;
                this.$refs.stage.getStage().draw();
            }, 1000);
        },
        updateLine() {
            for (let l in this.links) {
                this.allLinks.pop()
            }
            const ll = this.$refs.lineLayer.getNode();
            const stage = vm.$refs.stage.getNode();
            // ll.draw();
            stage.draw();
        },
        handleDragstart(e) {
            const shape = e.target;
            const dragLayer = vm.$refs.dragLayer.getNode();
            const stage = vm.$refs.stage.getNode();
            // moving to another layer will improve dragging performance
            shape.moveTo(dragLayer);
            stage.draw();
        },
        handleDragend(e) {
            const shape = e.target;
            const layer = vm.$refs.layer.getNode();
            const stage = vm.$refs.stage.getNode();
            shape.moveTo(layer);
            stage.draw();
            shape.attrs.x = shape.getAttr("x");
            shape.attrs.y = shape.getAttr("y");
            this.eachNodePoints[shape.attrs.name] = {
                x: shape.attrs.x,
                y: shape.attrs.y
            };
            alert(shape.attrs.x + " - " + shape.attrs.y);
            this.updateLine();
        }
    },
    components: {
        HamburgerButton
    },
    created() {
        // setInterval(() => {
        //     this.$store.dispatch("loadDevices");
        // }, 5000);
        this.$store.dispatch("loadDevices");
        this.$store.dispatch("loadNodeLinks");
        console.log("created");
    },
    mounted() {
        vm = this;
        EventBus.$on("clicked", data => {
            this.isActive = data;
            this.stageResize();
        });
        this.configKonva.width = this.$el.clientWidth;
        this.configKonva.height = this.$el.clientHeight;
        console.log("mounted");
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