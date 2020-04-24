import React from "react";
import PropTypes from "prop-types";
import withStyles from "@material-ui/core/styles/withStyles";
import classNames from "classnames";

import cardBodyStyle from "./cardBodyStyle.jsx";

function CardBody({ ...props }) {
    const { classes, className, children, plain, profile, ...rest } = props;
    const cardBodyClasses = classNames({
      [classes.cardBody]: true,
      [classes.cardBodyPlain]: plain,
      [classes.cardBodyProfile]: profile,
      [className]: className !== undefined
    });
    return (
      <div className={cardBodyClasses} {...rest}>
        {children}
      </div>
    );
  }
  
  CardBody.propTypes = {
    classes: PropTypes.object.isRequired,
    className: PropTypes.string,
    plain: PropTypes.bool,
    profile: PropTypes.bool,
    children: PropTypes.node
  };
  
  export default withStyles(cardBodyStyle)(CardBody);