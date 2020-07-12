<template>
  <div id="modifyattd-form">
    <b-form @submit.prevent="validate">
    <label>Prof/TA ID</label>
    <b-input :state='midstate' placeholder = "Enter New Marker ID.Must be a TA or Prof"
    v-model = 'modattd.mid'>
    </b-input>
    <br>

    <label>Student ID</label>
    <b-input :state='sidstate' placeholder = "Enter New Student ID" v-model = 'modattd.sid'>
    </b-input>
    <br>

    <label>Course ID</label>
    <b-input :state='cidstate' placeholder = "Enter new Course ID" v-model = 'modattd.cid'>
    </b-input>
    <br>

    <label>TimeStamp(Date of class) </label>
    <b-input type='date' :state='timdstate' placeholder = "Enter new Timestamp"
    v-model = 'modattd.timestamp'>
    </b-input>
    <br>

    <b-button type="submit"> Modify attendance record </b-button>
    </b-form>
  </div>
</template>

<script>
export default {
  name: 'ModifyAttdform',
  props: { attdrec: Array },
  data() {
    return {
      modattd: {
        mid: this.attdrec.taid || this.attdrec.fid || '',
        sid: this.attdrec.sid || '',
        cid: this.attdrec.cid || '',
        timestamp: this.attdrec.timestamp || '',
      },
    };
  },
  computed: {
    midstate() {
      return this.modattd.mid.length > 0;
    },
    sidstate() {
      return this.modattd.sid.length > 0;
    },
    cidstate() {
      return this.modattd.cid.length > 0;
    },
    timdstate() {
      return this.modattd.timestamp.length > 0;
    },
  },
  methods: {
    validate() {
      let f = 0;
      if (this.modattd.mid === null || this.modattd.mid === '') {
        f = 1;
      }
      if (this.modattd.sid === null || this.modattd.sid === '') {
        f = 1;
      }
      if (this.modattd.cid === null || this.modattd.cid === '') {
        f = 1;
      }
      if (this.modattd.timestamp === null || this.modattd.timestamp === '') {
        f = 1;
      }
      if (f === 0) {
        this.$emit('attdupd', this.modattd);
      }
    },
  },
};
</script>
