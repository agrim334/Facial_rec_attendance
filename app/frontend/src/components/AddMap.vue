<template>
  <div id="register-form">
    <form @submit.prevent="handle">
    <label>map ID</label>
    <input type="text" placeholder = "Enter CID" v-model = 'map.cid' />
    <br>

    <label>map name</label>
    <input type="text" placeholder = "Enter UID" v-model = 'map.uid' />
    <br>

    <label>map name</label>
    <input type="text" placeholder = "Enter User Role" v-model = 'map.role' />
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
        cid: '', uid: '', role: '',
      },
    };
  },
  methods: {
    handle() {
      this.$emit('mapadd', this.map);
    },
  },
};
</script>
