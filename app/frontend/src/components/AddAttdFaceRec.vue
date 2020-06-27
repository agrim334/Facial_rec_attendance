<template>
  <div id="register-form">
    <b-form @submit.prevent="validate">
    <label>User ID</label>
    <b-input :state='uidstate' placeholder = "Enter UID" v-model = 'attdrec.uid'>
    </b-input>
    <br>

    <label>Course ID</label>
    <b-input :state='cidstate' placeholder = "Enter CID" v-model = 'attdrec.cid'>
    </b-input>
    <br>

    <label> Class Image </label>
    <b-form-file v-model="files" id="files" ref="files" accept="image/*" multiple>
    </b-form-file>
    <br>

    <b-button type="submit"> Mark Attendance </b-button>
    </b-form>
  </div>
</template>

<script>
export default {
  name: 'MarkAttdFaceForm',
  props: { user: String },
  data() {
    return {
      attdrec: {
        uid: '',
        cid: '',
      },
      files: Array,
    };
  },
  computed: {
    uidstate() {
      return this.attdrec.uid.length > 0;
    },
    cidstate() {
      return this.attdrec.cid.length > 0;
    },
  },
  methods: {
    validate() {
      let f = 0;
      if (this.attdrec.uid === null || this.attdrec.uid === '') {
        alert('enter uid');
        f = 1;
      }
      if (this.attdrec.cid === null || this.attdrec.cid === '') {
        alert('enter cid');
        f = 1;
      }
      this.files = this.$refs.files.files;
      if (f === 0) {
        this.$emit('attdmark', { rec: this.attdrec, img: this.files });
      }
    },
  },
};
</script>
