import React from "react";
import PropTypes from "prop-types";
import withStyles from "@material-ui/core/styles/withStyles";
import Grid from "@material-ui/core/Grid";


const style={
    grid: {
        margin:"0 -15px !important",
        width: "unset"
    }
};

function GridItem({...props}) {
    const {classes,children, ...rest}=props;
    return (
        <Grid item {...rest} className={classes.grid}>
            {children}
        </Grid>
    );
}

GridItem.propTypes={
    classes: PropTypes.object,
    children: PropTypes.node
};

export default withStyles(style)(GridItem);