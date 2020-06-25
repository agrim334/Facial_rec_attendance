<template>
  <div id="register-form">
    <form @submit.prevent="handle">
    <label>map ID</label>
    <input type="text" placeholder = "Enter CID" v-model = 'map.cid' />
    <br>

    <label>map name</label>
    <input type="text" placeholder = "Enter UID" v-model = 'map.uid' />
    <br>

    <input type="submit" value="modify map" />
    </form>
  </div>
</template>

<script>
export default {
  name: 'AddMapForm',
  props: { ogmap: Array, roles: Array },
  data() {
    return {
      map: {
        cid: this.ogmap.cid,
        uid: this.ogmap.uid,
      },
    };
  },
  methods: {
    handle() {
      this.$emit('mapupd', this.map);
    },
  },
  created() {
    console.log(this.roles);
  },
};
</script>
