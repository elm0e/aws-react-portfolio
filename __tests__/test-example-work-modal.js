
import { configure } from 'enzyme';
import Adapter from 'enzyme-adapter-react-15';
configure({ adapter: new Adapter() });

import React from 'react';
import { shallow } from 'enzyme';
import ExampleWorkModal from '../js/example-work-modal';

const myExample = {
  'title': "Work Example",
  'href': "https://example.com",
  'desc': "description goes here",
  'image': {
    'desc': "example screenshot of a project involving code",
    'src': "images/example1.png",
    'comment': ""
  }
};

describe("ExampleWorkModal component", () => {
  let component = shallow(<ExampleWorkModal example={myExample} open={false} />);
  let openComponent = shallow(<ExampleWorkModal example={myExample} open={true} />);
  let anchors = component.find('a');

  it("Should contain a single 'a' element", () => {
    expect(anchors.length).toEqual(1);
  });
  it("Should link to our project", () => {
    expect(anchors.getElement(0).props.href).toEqual(myExample.href);
  });
  it("Should have the modal class set correctly", () => {
    expect(component.find('.background--skyBlue').hasClass('modal--closed')).toBe(true);
    expect(openComponent.find('.background--skyBlue').hasClass('modal--open')).toBe(true);
  });
});
