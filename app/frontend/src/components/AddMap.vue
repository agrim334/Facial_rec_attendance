<template>
  <div id="register-form">
    <form @submit.prevent="handle">
    <label>map ID</label>
    <input type="text" placeholder = "Enter CID" v-model = 'map.cid' />
    <br>

    <label>map name</label>
    <input type="text" placeholder = "Enter UID" v-model = 'map.uid' @change = 'getusertype' />
    <br>

    <div v-if='map.role === 1'>
      <label> Student Image </label>
      <input type="file" accept="image/*" id="file-input">
    </div>
    <br>

    <input type="submit" value="Add map" />
    </form>
  </div>
</template>

<script>

export default {
  name: 'AddMapForm',
  props: { roles: Array },
  data() {
    return {
      map: {
        cid: '', uid: '',
      },
    };
  },
  methods: {
    handle() {
      let f = 0;
      if (this.map.id === null || this.map.id === '') {
        alert('fill map id');
        f = 1;
      }
      if (this.map.name === null || this.map.name === '') {
        alert('fill map name');
        f = 1;
      }
      if (f === 0 ) {
        this.$emit('mapadd', this.map);
      }
    },
  },
};
</script>
