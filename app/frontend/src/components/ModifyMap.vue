<template>
  <div id="register-form">
    <form @submit.prevent="validate">
    <label>map ID</label>
    <input type="text" placeholder = "Enter CID" v-model = 'map.cid' />
    <br>

    <label>map name</label>
    <input type="text" placeholder = "Enter UID" v-model = 'map.uid' />
    <br>

    <input type="submit" value="Modify map" />

     <form id="addimg" v-if='isstud.val === 1' @submit.prevent='uplimg'>
      <div >
        <label> Student Image </label>
        <input type="file" id="file" ref="file" accept="image/*" />
      </div>
      <input type="submit" value="Upload new image" />
    </form>
  </form>

  </div>
</template>

<script>
export default {
  name: 'ModifyMapForm',
  props: { ogmap: Object, isstud: Object },
  data() {
    return {
      map: {
        cid: this.ogmap.cid,
        uid: this.ogmap.uid,
      },
      file: '',
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
    uplimg() {
      [this.file] = this.$refs.file.files;
      this.$emit('imgupl', { img: this.file, uid: this.map.uid });
    },
  },
};
</script>
