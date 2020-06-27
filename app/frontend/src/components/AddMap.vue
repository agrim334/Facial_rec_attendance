<template>
  <div id="register-form">
    <b-form @submit.prevent="validate" v-if='isstud === 0'>
    <label>User ID</label>
    <b-input :state='uidstate' placeholder = "Enter UID" v-model = 'map.uid'>
    </b-input>
    <br>

    <label>Course ID</label>
    <b-input :state='cidstate' placeholder = "Enter CID" v-model = 'map.cid'>
    </b-input>
    <br>

    <b-button type="submit"> Add map </b-button>
    </b-form>
    <b-form id="addimg" v-if='isstud === 1' @submit.prevent='uplimg'>
      <label> Student Image </label>
        <b-form-file v-model="file" id="fileupl" ref="studimg" accept="image/*">
        </b-form-file>
      <b-button type="submit"> Add image </b-button>
    </b-form>
  </div>
</template>

<script>

export default {
  name: 'AddMapForm',
  props: { isstud: Object },
  data() {
    return {
      map: {
        cid: '', uid: '',
      },
      file: null,
    };
  },
  computed: {
    uidstate() {
      return this.map.uid.length > 0;
    },
    cidstate() {
      return this.map.cid.length > 0;
    },
  },
  methods: {
    validate() {
      let f = 0;
      if (this.map.cid === null || this.map.cid === '') {
        alert('fill map course id');
        f = 1;
      }
      if (this.map.uid === null || this.map.uid === '') {
        alert('fill map user id');
        f = 1;
      }
      if (f === 0) {
        this.$emit('mapadd', this.map);
      }
    },
    uplimg() {
      this.$emit('imgupl', { img: this.file, dat: this.map });
    },
  },
};
</script>
