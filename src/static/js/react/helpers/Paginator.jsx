/**
 * Created by yuehaitao on 2016/11/8.
 */
import React from 'react';
import ReactPaginate from 'react-paginate';

const Paginator = ({ pagination, pages, onSelect }) => (
    <ReactPaginate previousLabel={"previous"}
                   nextLabel={"next"}
                   breakLabel={<a href="javascript:void(0)">...</a>}
                   breakClassName={"break-me"}
                   pageNum={pages}
                   marginPagesDisplayed={2}
                   pageRangeDisplayed={5}
                   clickCallback={onSelect}
                   containerClassName={"pagination"}
                   subContainerClassName={"pages pagination"}
                   activeClassName={"active"} />
);
Paginator.propTypes = {
  pagination: React.PropTypes.object,
  pages: React.PropTypes.number,
  onSelect: React.PropTypes.func
};

export default Paginator;
