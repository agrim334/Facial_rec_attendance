<template>
  <div id="register-form">
    <form @submit.prevent="handle">
    <label>map ID</label>
    <input type="text" placeholder = "Enter CID" v-model = 'map.cid' />
    <br>

    <label>map name</label>
    <input type="text" placeholder = "Enter UID" v-model = 'map.uid' />
    <br>

    <label>Role</label>
    <div id = 'rolerad' v-for='role in roles' :key='role.id'>
      <input type="radio" name= 'role.name' :value = 'role.id' v-model = 'map.role'>
      <label> {{ role.name }} </label>
    </div>
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
  props: { ogmap: Array, roles: Array },
  data() {
    return {
      map: {
        cid: this.ogmap.cid,
        id: this.ogmap.id,
        role: this.ogmap.role,
      },
    };
  },
  methods: {
    handle() {
      this.$emit('mapadd', this.map);
    },
  },
  created() {
    console.log(this.roles);
  },
};
</script>
