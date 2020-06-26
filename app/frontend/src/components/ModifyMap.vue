<template>
  <div id="register-form">
    <form @submit.prevent="validate">
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
    validate() {
      let f = 0;
      if (this.map.cid === null || this.map.cid === '') {
        alert('fill Course ID');
        f = 1;
      }
      if (this.map.uid === null || this.map.uid === '') {
        alert('fill User ID');
        f = 1;
      }
      if (f === 0) {
        this.$emit('mapupd', this.map);
      }
    },
  },
};
</script>
